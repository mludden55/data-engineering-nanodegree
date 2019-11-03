from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    insert_sql = """
        INSERT INTO {}
        {};
        COMMIT;
    """

    truncate_sql = """
        DELETE FROM
        {};
        COMMIT;
    """
    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id='',
                 table='',
                 load_sql='',
                 mode = '',
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.load_sql = load_sql
        self.mode = mode

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("Loading dimension table {}".format(self.table))

        if self.mode == 'append':
            formatted_sql = LoadDimensionOperator.insert_sql.format(
                self.table,
                self.load_sql
            )
        else:
            formatted_sql = LoadDimensionOperator.truncate_sql.format(
                self.table
            )
            formatted_sql += LoadDimensionOperator.insert_sql.format(
                self.table,
                self.load_sql
            )
        self.log.info("Formatted SQL {}".format(formatted_sql))
        redshift.run(formatted_sql)
