from fastapi import APIRouter

from .routers import auth, admin, users, employee, client, event, detail_event
router = APIRouter()

router.include_router(router=auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(router=admin.router, prefix="/admin", tags=["Admin"])
router.include_router(router=employee.router, prefix="/employee", tags=["Employee"])
router.include_router(router=client.router, prefix="/client", tags=["Client"])
router.include_router(router=event.router, prefix="/event", tags=["Event"])
router.include_router(router=detail_event.router, prefix="/detail_event", tags=["Detail_event"])
router.include_router(router=users.router, prefix="/users", tags=["Users"])

