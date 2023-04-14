const {MongoClient} = require('mongodb');
const mongoDbUri = process.env.MONGODB_URI;
const client = new MongoClient(mongoDbUri);
const oldDb = process.env.OLD_DB_NAME;
const newDb = process.env.NEW_DB_NAME;
const collectionName = process.env.COLLECTION_NAME;
const batchSize = 1000;


async function main() {
    try {
        //connect to old and new collections
        console.log('***Connecting to DB***');
        await client.connect();
        console.log('***Connected to DB***');
        var oldDatabase = client.db(oldDb);
        var oldCollection = oldDatabase.collection(collectionName);
        var newDatabase = client.db(newDb);
        var newCollection = newDatabase.collection(collectionName);

        // First copy the collection
        await copyCollection(oldCollection, newCollection);
        //Only when the collection is being copied apply the triggers.
        await aplyTriggers(oldCollection, newCollection);
    } catch (e) {
        console.error(e);
    }
}

main().catch(console.error);

async function copyCollection(oldCollection, newCollection) {
    console.log('***Start copying Collection***');

    // delete all entries from collection
    await newCollection.deleteMany();

    // copy  contents from old collection to the new one
    const cursor = oldCollection.find().batchSize(batchSize);
    let batch = [];
    let count = 0;
    while (await cursor.hasNext()) {
        const document = await cursor.next();
        batch.push({insertOne: {document}});
        count++;
        if (batch.length === batchSize) {
            try {
                await newCollection.bulkWrite(batch);
                console.log(`Inserted ${count} documents`);
            } catch (e) {
                console.log(`***Skipping ${count} documents***`);
                console.error(e)
            }
            batch = [];
        }
    }
    if (batch.length > 0) {
        try {
            await newCollection.bulkWrite(batch);
            console.log(`Inserted ${count} documents`);
        } catch (e) {
            console.log(`***Skipping ${count} documents***`);
            console.error(e)
        }
    }
    console.log('***Copying Collection operation finished***');
}

async function aplyTriggers(oldCollection, newCollection) {
    console.log('***Start applying triggers***');

    // create a change stream for insert operations
    const insertStream = oldCollection.watch([{$match: {operationType: 'insert'}}]);
    await insertStream.on('change', function (change) {
        console.log('New document inserted:', change.fullDocument);
        newCollection.insertOne(change.fullDocument);
    });
    // create a change stream for update operations
    const updateStream = oldCollection.watch([{$match: {operationType: 'update'}}]);
    await updateStream.on('change', function (change) {
        console.log('Document updated:', change.documentKey);
        newCollection.updateOne(change.fullDocument);
    });
    // create a change stream for update operations
    const replaceStream = oldCollection.watch([{$match: {operationType: 'replace'}}]);
    await replaceStream.on('change', function (change) {
        console.log('Document replaced:', change.fullDocument);
        newCollection.replaceOne(change.documentKey, change.fullDocument);
    });
    // create a change stream for delete operations
    const deleteStream = oldCollection.watch([{$match: {operationType: 'delete'}}]);
    await deleteStream.on('change', function (change) {
        console.log('Document deleted:', change.documentKey);
        newCollection.deleteOne(change.documentKey);
    });
    console.log('***TRIGGERS SUCCESSFULLY APPLIED***');
}