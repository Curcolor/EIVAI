"""
Archivo principal para ejecutar el servidor FastAPI con tareas en segundo plano
"""
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from src.api.app import create_app
from src.utils.background_tasks import start_background_tasks, stop_background_tasks


@asynccontextmanager
async def lifespan(app):
    """
    Gestor del ciclo de vida de la aplicación
    """
    # Inicialización: iniciar tareas en segundo plano
    task = asyncio.create_task(start_background_tasks())
    
    try:
        yield
    finally:
        # Limpieza: detener tareas en segundo plano
        await stop_background_tasks()
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


app = create_app()
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
