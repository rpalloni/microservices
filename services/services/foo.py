from services.schemas.foo import FooItemCreate
from services.services.main import AppService, AppCRUD
from services.models.foo import FooItem
from services.utils.service_result import ServiceResult
from services.utils.app_exceptions import AppException


class FooService(AppService):
    def create_item(self, item: FooItemCreate) -> ServiceResult:
        foo_item = FooCRUD(self.db).create_item(item)
        if not foo_item:
            return ServiceResult(AppException.FooCreateItem())
        return ServiceResult(foo_item)

    def get_item(self, item_id: int) -> ServiceResult:
        foo_item = FooCRUD(self.db).get_item(item_id)
        if not foo_item:
            return ServiceResult(AppException.FooGetItem({"item_id": item_id}))
        if not foo_item.public:
            return ServiceResult(AppException.FooItemRequiresAuth())
        return ServiceResult(foo_item)


class FooCRUD(AppCRUD):
    def create_item(self, item: FooItemCreate) -> FooItem:
        foo_item = FooItem(description=item.description, public=item.public)
        self.db.add(foo_item)
        self.db.commit()
        self.db.refresh(foo_item)
        return foo_item

    def get_item(self, item_id: int) -> FooItem:
        foo_item = self.db.query(FooItem).filter(FooItem.id == item_id).first()
        if foo_item:
            return foo_item
        return None
