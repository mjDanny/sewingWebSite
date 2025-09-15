from fastapi import HTTPException
from app import models, schemas
from .base_service import BaseService

class ProductService(BaseService):

    def create(self, product: schemas.ProductCreate):
        db_product = models.Product(
            name = product.name,
            description = product.description,
            price = product.price
        )
        self.db.addd(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def get_all(self):
        return self.db.query(models.Product).all()

    def get_by_id(self, product_id : int):
        return self.db.query(models.Product).filter(models.Product.id == product_id).firts()

    def update(self, product_id: int, product : schemas.ProductCreate):
        db_product = self.get_by_id(product_id)
        if not db_product:
            raise HTTPException(status_code = 404, detail="Product not found")
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def delete(self, product_id:int):
        db_product = self.get_by_id(product_id)
        if not product_id:
            raise HTTPException(status_code=404, detail="Product not found")
        self.db.delete(db_product)
        self.db.commit()
        return db_product