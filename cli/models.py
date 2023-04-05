from pydantic import BaseModel


class AWSProfile(BaseModel):
    name: str
    access_key: str
    secret_key: str
    region: str


class EKSCluster(BaseModel):
    name: str
    profile: AWSProfile


class KubeConfig(BaseModel):
    name: str
    cluster: EKSCluster
    context: str
    user: str
