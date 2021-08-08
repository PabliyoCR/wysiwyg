import graphene
import wysiwyg.schema


class Query(wysiwyg.schema.Query, graphene.ObjectType):
    pass


class Mutation(wysiwyg.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
