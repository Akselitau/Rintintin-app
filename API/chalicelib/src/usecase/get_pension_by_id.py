from chalice import Response
from chalicelib.src.bootstrap import get_pension_repo

from chalice import Response
from chalicelib.src.bootstrap import get_pension_repo

def get_pension_by_id_handler(pension_id):
    try:
        pension_repo = get_pension_repo()
        result = pension_repo.get_pension_by_id(pension_id)
        
        if result is None:
            return Response(
                body={"message": "Pension not found"},
                status_code=404,
                headers={"Content-Type": "application/json"}
            )
                
        return Response(
            body=result.dict(),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"An error occurred: {e}")  # Debugging print
        return Response(
            body={"message": f"An error occurred: {e}"},
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
