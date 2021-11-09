from abc import ABC, abstractmethod

from flask.views import MethodView
from mongoengine import Document


# FIXME: Not finished, possibly not even remotely useful
#        this was an idea to try and completely abstract
#        api CRUD for any model
#        It should definitely be easier to just create
#        flask.views.MethodView for each model manually
#        and after that, see if these vies share some code
#        and then abstract to functions/classes that

class DocumentResourceBaseHandler(ABC):
    """
    Base class for all document resources

    Document resource has to do exactly three actions
    - POST      - create document (C[reate])
    - GET       - view document   (R[ead])
    - PUT       - update document (U[pdate])
    - DELETE    - delete document (D[elete])

    NOTE: This is a heavy abstraction that tried to
    create single CRUD handler for any mongo model.

    Main requirement of this was to verify that
    request arguments (ex.: POST /models/host?name=test?field=value)
    does contains only valid fields for the model in question
    and there is absolutely no other stuff (for security reasons,
        so that the parsed values can be then **spread as in Model.objects.create(**kwargs)
        with passing additional arguments to it)

    Unresolved problems:
        - how to decide which fields can be supplied from args
            and which fields are hidden and shouldn't be touched like this
        - how to handle, for any model, embedded and reference fields
            - one idea would be to do introspection ( isinstance(..., ReferenceField) )
            on all the fields of the said model and if it's one of these two, use the provided value
            (host.cloud="cloud_name") to first get the reference model.
    """
    model: Document

    @staticmethod
    def make_url_parser(model: Document):
        """
        Creates a URL param parser for any model's fields
        :param model:
        :return:
        """
        pass

    def GET(self):
        """
        View document
        """
        pass

    def POST(self):
        """
        Create (add) document
        """
        pass

    def PUT(self):
        """
        Update document
        """
        pass

    def DELETE(self):
        """
        Delete document
        """
        pass

    @abstractmethod
    def coalesce(self) -> dict:
        # subclasses have to implement this
        pass


# Example, not tested at all
class HostResource(DocumentResourceBaseHandler, MethodView):
    def coalesce(self) -> dict:
        pass


class DocumentResourceFactory:
    def __call__(self, document: Document):
        return type(DocumentResourceBase)
