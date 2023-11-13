/* Example SAS code to connect to Databricks using DBCONNECT */

/* Set your Databricks connection parameters */
%let db_host = <Databricks_Hostname>;
%let db_port = <Databricks_Port>;
%let db_token = <Databricks_Auth_Token>;

/* Define the DSN (Data Source Name) for Databricks */
%let dsn = DATABRICKS;

/* Connect to Databricks using DBCONNECT */
proc dbconnect
  class=DATABRICKS
  init_string="Host=&db_host. Port=&db_port. AuthToken=&db_token."
  ;
  
  /* Your SAS code for data manipulation goes here */
  /* For example, you can use SQL queries or data step code */
  
/* Disconnect from Databricks */
disconnect from DATABRICKS;
run;
