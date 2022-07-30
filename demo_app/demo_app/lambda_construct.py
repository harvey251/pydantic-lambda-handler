from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from constructs import Construct


class LambdaConstruct(Construct):

    # @property
    # def buckets(self):
    #     return tuple(self._buckets)

    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)
        # self._buckets = []
        # for i in range(0, num_buckets):
        #     self._buckets.append(s3.Bucket(self, f"Bucket-{i}"))

    # def grant_read(self, principal: iam.IPrincipal):
    #     for b in self.buckets:
    #         b.grant_read(principal, "*")
