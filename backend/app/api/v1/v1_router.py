from fastapi import APIRouter, Depends

from .routers import auth, admin, users, employee
router = APIRouter()

router.include_router(router=auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(router=admin.router, prefix="/admin", tags=["Admin"])
router.include_router(router=employee.router, prefix="/employee", tags=["Employee"])
router.include_router(router=users.router, prefix="/users", tags=["Users"])

# router.include_router(router=me.router, tags=["self"])

#
# router.include_router(
#     router=roles.router,
#     prefix="/roles",
#     tags=["roles"],
#     dependencies=[Depends(admin_role)],
# )

# router.include_router(router=shops.router, prefix="/shops", tags=["shops"])