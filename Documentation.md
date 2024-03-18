# API Documentation

# Create User

- Endpoint

<aside>
💡 *http://localhost:8000/api/user*

</aside>

- Method Type

<aside>
💡 POST

</aside>

- Body

```jsx
{
	username: str,
	first_name: str,
	last_name: str, //Optional
	email: str,
	password: str
}
```

- Response
    - Status Codes
        - 201 - Created Successfully
        - 400 - Incomplete Request Body
        - 409 - Given Username already exists

# Login User

- Endpoint

<aside>
💡 *http://localhost:8000/api/auth*

</aside>

- Method Type

<aside>
💡 POST

</aside>

- Body

```jsx
{
	username: str,
	password: str
}
```

- Response
    - Status Codes
        - 200 - Login Successful
        
        ```jsx
        body = {
        				access: str,
        				refresh: str
        }
        ```
        
        - 400 - Incomplete Request Body
        - 401 - Incorrect Credentials

# Delete User

- Endpoint

<aside>
💡 *http://localhost:8000/api/user*

</aside>

- Method Type

<aside>
💡 DELETE

</aside>

- Headers

```jsx
{
	Authorization: Bearer {access token}
}
```

- Response
    - Status Codes
        - 204 - Deleted Successfully
        - 401 - Unauthorized (Incorrect Access Token)
        - 500 - Server Error

# Create Task

- Endpoint

<aside>
💡 *http://localhost:8000/api/task*

</aside>

- Method Type

<aside>
💡 POST

</aside>

- Headers

```jsx
{
	Authorization: Bearer {access token}
}
```

- Body

```jsx
{
	title: str,
	description: str, //Optional
	deadline: str //format = yyyy-mm-dd HH-MM-SS.msTZ eg: 2024-03-22T16:30:00.0000+05:30
}
```

- Response
    - Status Codes
        - 201 - Created Successfully
        
        ```jsx
        body = {
        	id: int,
        	title: str,
        	description: str/null,
        	createdOn: str, //format = yyyy-mm-dd HH-MM-SS.msTZ eg: 2024-03-22T16:30:00.0000+05:30
        	deadline: str, //format = yyyy-mm-dd HH-MM-SS.msTZ eg: 2024-03-22T16:30:00.0000+05:30
        	username: str,
        	complete: bool
        }
        ```
        
        - 400 - Incomplete Request Body
        - 401 - Unauthorized (Incorrect Access Token)

# Get Task

## Get All Tasks

- Endpoint

<aside>
💡 *http://localhost:8000/api/task*

</aside>

- Method Type

<aside>
💡 GET

</aside>

- Headers

```jsx
{
	Authorization: Bearer {access token}
}
```

- Response
    - Status Codes
        - 200 - Success
        
        ```jsx
        body = [{
        	id: int,
        	title: str,
        	description: str/null,
        	createdOn: str, //format = yyyy-mm-dd HH-MM-SS.msTZ eg: 2024-03-22T16:30:00.0000+05:30
        	deadline: str, //format = yyyy-mm-dd HH-MM-SS.msTZ eg: 2024-03-22T16:30:00.0000+05:30
        	username: str,
        	complete: bool
        }, ...]
        ```
        
        - 401 - Unauthorized (Incorrect Access Token)

## Get Specific Task

- Endpoint

<aside>
💡 *http://localhost:8000/api/task?id={task_id}*

</aside>

- Method Type

<aside>
💡 GET

</aside>

- Headers

```jsx
{
	Authorization: Bearer {access token}
}
```

- Response
    - Status Codes
        - 200 - Success
        
        ```jsx
        body = {
        	id: int,
        	title: str,
        	description: str/null,
        	createdOn: str, //format = yyyy-mm-dd HH-MM-SS.msTZ eg: 2024-03-22T16:30:00.0000+05:30
        	deadline: str, //format = yyyy-mm-dd HH-MM-SS.msTZ eg: 2024-03-22T16:30:00.0000+05:30
        	username: str,
        	complete: bool
        }
        ```
        
        - 401 - Unauthorized (Incorrect Access Token)
        - 404 - Not Found

# Update Task

- Endpoint

<aside>
💡 *http://localhost:8000/api/task?={task_id}*

</aside>

- Method Type

<aside>
💡 PUT

</aside>

- Headers

```jsx
{
	Authorization: Bearer {access token}
}
```

- Body

```jsx
{
	title: str,
	description: str, //Optional
	deadline: str //format = yyyy-mm-dd HH-MM-SS.msTZ eg: 2024-03-22T16:30:00.0000+05:30
}
```

- Response
    - Status Codes
        - 204 - Updated Successfully
        - 400 - Incomplete Request Body or URL parameter (id)
        - 401 - Unauthorized (Incorrect Access Token)
        - 404 - Task Not Found

# Update Task Status

- Endpoint

<aside>
💡 *http://localhost:8000/api/task?={task_id}*

</aside>

- Method Type

<aside>
💡 PATCH

</aside>

- Headers

```jsx
{
	Authorization: Bearer {access token}
}
```

- Body

```jsx
{
	complete: bool
}
```

- Response
    - Status Codes
        - 204 - Updated Successfully
        - 400 - Incomplete Request Body or URL Parameter (id)
        - 401 - Unauthorized (Incorrect Access Token)
        - 404 - Task Not Found

# Delete Task

- Endpoint

<aside>
💡 *http://localhost:8000/api/task?id={task_id}*

</aside>

- Method Type

<aside>
💡 DELETE

</aside>

- Headers

```jsx
{
	Authorization: Bearer {access token}
}
```

- Response
    - Status Codes
        - 204 - Success
        - 401 - Unauthorized (Incorrect Access Token)
        - 404 - Not Found