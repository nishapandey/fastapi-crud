#create
curl -X POST "http://127.0.0.1:8000/posts"   -H "Content-Type: application/json"   -d '{"title": "4th post", "content": "Hello world"}'

#delete
curl -X DELETE "http://127.0.0.1:8000/posts/1"

#update
curl -X PUT "http://127.0.0.1:8000/posts/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "5th post", "content": "This content was updated"}'

#get
curl -X GET "http://127.0.0.1:8000/posts/1"

#documentation http://127.0.0.1:8000/docs

#login
curl -X POST "http://127.0.0.1:8000/users"   -H "Content-Type: application/json"   -d '{"email": "email@gmai.com", "password": "password123"}'

#get
curl -X GET "http://127.0.0.1:8000/users" 

curl -X POST "http://127.0.0.1:8000/login"   -H "Content-Type: application/json"   -d '{"email": "email@gmail.com", "password": "password123"}'