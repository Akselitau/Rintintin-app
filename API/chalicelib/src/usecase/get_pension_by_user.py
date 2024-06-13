from chalice import Response

from chalicelib.src.bootstrap import get_pension_repo

def get_pension_by_user_handler(user_id):
    try:
        pension_repo = get_pension_repo()
        result = pension_repo.get_pension_by_user_id(user_id)
        
        if "message" in result:
            status_code = 404 if result["message"] == "Pension not found" else 500
            return Response(
                body=result,
                status_code=status_code,
                headers={"Content-Type": "application/json"}
            )
        else:
            return Response(
                body=result,
                status_code=200,
                headers={"Content-Type": "application/json"}
            )
    except Exception as e:
        return Response(
            body={"message": f"An error occurred: {e}"},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
