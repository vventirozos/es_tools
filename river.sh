curl -XPUT 'localhost:9200/_river/my_jdbc_river/_meta' -d '{
"type" : "jdbc",
"jdbc" : {
"url" : "jdbc:postgresql://localhost:5432/monkey_river",
"user" : "postgres",
"password" : "",
"sql" : "select * from test;"
	}
}'
