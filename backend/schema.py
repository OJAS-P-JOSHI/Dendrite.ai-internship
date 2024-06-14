import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import ToDoModel, session

class ToDoObject(SQLAlchemyObjectType):
    class Meta:
        model = ToDoModel
        interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_todos = SQLAlchemyConnectionField(ToDoObject)

class CreateToDo(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        time = graphene.String(required=True)
        image = graphene.String()

    todo = graphene.Field(lambda: ToDoObject)

    def mutate(self, info, title, description, time, image=None):
        todo = ToDoModel(title=title, description=description, time=time, image=image)
        session.add(todo)
        session.commit()
        return CreateToDo(todo=todo)

class Mutation(graphene.ObjectType):
    create_todo = CreateToDo.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
