from fastapi import Request, Response
from traffix.main import templates
from traffix.models import Alert


def render_alert(
    request: Request, colour: str, title: str, text: str, status_code: int = 200
) -> Response:
    alert = Alert(colour=colour, title=title, text=text)
    return templates.TemplateResponse(
        name="fragments/alert.html",
        context={"request": request, "alert": alert},
        status_code=status_code,
    )
