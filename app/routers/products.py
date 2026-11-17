from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.products import Product as ProductModel
from app.models.categories import Category as CategoryModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.db_depends import get_db


# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductSchema:
    """
    Проверка существования товара
    :param product_id:
    :param db:
    :return: Выборка по товару db_product
    """
    db_product = db.scalars(select(ProductModel)
                            .where(ProductModel.is_active == True,
                                   ProductModel.id == product_id)
                            ).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return db_product


def get_caterogy(category_id: int, db: Session = Depends(get_db)) -> None:
    """
    Проверка существования категории
    :param category_id:
    :param db:
    :return: None
    """

    category = db.scalars(select(CategoryModel)
                          .where(CategoryModel.is_active == True,
                                 CategoryModel.id == category_id)
                          ).first()
    if category is None:
        raise HTTPException(status_code=400, detail="Parent category not found")

    return None


@router.get("/", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_all_products(db: Session = Depends(get_db)) -> Sequence[ProductSchema]:
    """
    Возвращает список всех товаров.
    """
    products = db.scalars(
        select(ProductModel)
        .where(ProductModel.is_active == True)
    ).all()
    return products


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)) -> ProductSchema:
    """
    Создаёт новый товар.
    """
    # Проверка существования категории
    get_caterogy(product.category_id, db)

    # Создание нового товара
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@router.get("/category/{category_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_products_by_category(category_id: int, db: Session = Depends(get_db) ) -> Sequence[ProductSchema]:
    """
    Возвращает список товаров в указанной категории по её ID.
    """
    get_caterogy(category_id, db)

    products = db.scalars(
        select(ProductModel)
        .where(ProductModel.is_active == True,
               ProductModel.category_id == category_id)
    ).all()
    return products


@router.get("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: Session = Depends(get_db)) -> Sequence[ProductSchema]:
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    db_product = get_product(product_id, db)

    return db_product


@router.put("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)) -> ProductSchema:
    """
    Обновляет товар по его ID.
    """
    # Проверка существования товара
    db_product = get_product(product_id, db)

    # Проверка существования категории
    get_caterogy(product.category_id, db)

    # Обновление товара
    db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(**product.model_dump())
    )
    db.commit()
    db.refresh(db_product)

    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Удаляет товар по его ID.
    """
    # Проверка существования товара
    product = get_product(product_id, db)

    # Удаление товара из активных
    # db.execute(update(ProductModel)
    #            .where(ProductModel.id == product_id)
    #            .values(is_active=False)
    # )
    product.is_active = False
    db.commit()
    return {"status": "success", "message": "Product marked as inactive"}
