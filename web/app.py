from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin,ModelView
from web.provider import UsernameAndPasswordProvider
from db.model import db,User,Product,Category,Order


app=Starlette()
admin=Admin(db._engine,
            title='P_29Admin',
            base_url='/',
            auth_provider=UsernameAndPasswordProvider(),
            middlewares=[Middleware(SessionMiddleware, secret_key="sdgfhjhhsfdghn")]
)
admin.add_view(ModelView(User))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Product))
admin.add_view(ModelView(Order))
admin.mount_to(app)