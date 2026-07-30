from fastapi import Depends, FastAPI, Query, status
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

from utils.response import ApiResponse


app = FastAPI()


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post(
    "/todos/", response_model=ApiResponse[Todo], status_code=status.HTTP_201_CREATED
)
def create_todo(todo: Todo, session: SessionDep) -> Todo:
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return ApiResponse(
        status_code=status.HTTP_201_CREATED,
        message="Todo created successfully",
        data=todo,
    )


@app.get(
    "/todos/", response_model=ApiResponse[list[Todo]], status_code=status.HTTP_200_OK
)
def read_todoes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Todo]:
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    return ApiResponse(
        message="Todos fetched successfully", data=todos, status_code=status.HTTP_200_OK
    )


@app.get(
    "/todos/{todo_id}", response_model=ApiResponse[Todo], status_code=status.HTTP_200_OK
)
def read_todo(todo_id: int, session: SessionDep) -> Todo:
    todo = session.get(Todo, todo_id)
    if not todo:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Todo not found",
                "data": None,
            },
        )

    return ApiResponse(
        status_code=status.HTTP_200_OK,
        message="Todo fetched successfully",
        data=todo,
    )


@app.delete(
    "/todos/{todo_id}",
    response_model=ApiResponse[Todo],
    status_code=status.HTTP_200_OK,
)
def delete_todo(todo_id: int, session: SessionDep):
    todo = session.get(Todo, todo_id)
    if not todo:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Todo not found",
                "data": None,
            },
        )
    session.delete(todo)
    session.commit()
    return ApiResponse(
        status_code=status.HTTP_200_OK,
        message="Todo deleted successfully",
        data=todo,
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Annotated[str | None, Query(max_length=50)] = None):
    return {"item_id": item_id, "q": q}
