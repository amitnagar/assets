from concurrent import futures
import random

import grpc

from entity_pb2 import (
    EntityRecord,
    EntityResponse,
)
import entity_pb2_grpc

# books_by_category = {
#     BookCategory.MYSTERY: [
#         BookRecommendation(id=1, title="The Maltese Falcon"),
#         BookRecommendation(id=2, title="Murder on the Orient Express"),
#         BookRecommendation(id=3, title="The Hound of the Baskervilles"),
#     ],
#     BookCategory.SCIENCE_FICTION: [
#         BookRecommendation(
#             id=4, title="The Hitchhiker's Guide to the Galaxy"
#         ),
#         BookRecommendation(id=5, title="Ender's Game"),
#         BookRecommendation(id=6, title="The Dune Chronicles"),
#     ],
# }

ent = {
        0:[EntityRecord(id=1, category="mortgage", entity="ent1"), EntityRecord(id=2, category="mortgage", entity="ent2"), EntityRecord(id=3, category="ethics", entity="ent3")],
        1:[EntityRecord(id=1, category="mortgage", entity="ent2")],
        2: [EntityRecord(id=1, category="mortgage", entity="ent3")],
}

class EntityService(
    entity_pb2_grpc.EntitiesServicer
):
    def extract(self, request, context):
        # if request.category not in books_by_category:
        #      context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
        # validate if document is there
        # then invoke custom entity extractor
        # get the entity list (category: entities) and create EntityRecord

        num_results = 3
        ent0 = ent[0]
        entities_to_recommend = random.sample(list(ent0), num_results)

        return EntityResponse(erecords=entities_to_recommend)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    entity_pb2_grpc.add_EntitiesServicer_to_server(
            EntityService(), server
        )
    server.add_insecure_port("[::]:50054")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()