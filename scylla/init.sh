#!/bin/bash
# Credits to: https://stackoverflow.com/a/76972678
echo "######### Starting to execute SH script... #########"

# If you have credentials for your DB uncomment the following two lines
# USER_NAME='user_name'
# PASSWORD='user_password'

for cql_file in ./scripts/*.cql;
do
# If you have credentials on your db use this line cqlsh scylla -u "${USER_NAME}" -p "${PASSWORD}" -f "${cql_file}" ;
  cqlsh scylla -f "${cql_file}" ;
  echo "######### Script ""${cql_file}"" executed!!! #########"
done
echo "######### Execution of SH script is finished! #########"
echo "######### Stopping temporary instance! #########"
