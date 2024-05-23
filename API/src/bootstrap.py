from chalice.infrastructure.pension_psql_repository import PsqlPensionRepository

psql_pension_repo = None

def get_pension_repo() -> PsqlPensionRepository:
    global psql_pension_repo
    if psql_pension_repo is None:
        psql_pension_repo = PsqlPensionRepository(
            host="database-1.cra8ueqsi8ry.eu-west-3.rds.amazonaws.com",
            port=5432,
            db_name="doggydb",
            user="aksel",
            password="changeme",
        )
    return psql_pension_repo
