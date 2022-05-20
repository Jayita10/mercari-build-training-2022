
1. [API and web service (the best for beginner)](https://mercari.udemy.com/course/api-and-web-service-introduction/)
2. [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
3. [Build-in json package in python](https://www.geeksforgeeks.org/python-json/)
4. [Sqlite3 in python](https://mercari.udemy.com/course/using-sqlite3-databases-with-python)
5. [Database normalization](https://docs.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description)
6. [loggers and log level](https://sematext.com/blog/logging-levels/)
7. [Port numbers](https://opensource.com/article/18/10/common-network-ports) || [video](https://www.youtube.com/watch?v=RDotMcs0Erg)
8. [Docker](https://docs.docker.com/get-started/overview/)
9. [HTTP status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
10. [HTTP request method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
11. [POST request using CURL](https://linuxize.com/post/curl-post-request/#:~:text=When%20the%20%2DF%20option%20is,form%2Durlencoded%20Content%2DType.)
12. [Docker Compose](https://docs.docker.com/compose/gettingstarted/)


* To format long queries, you should use triple quoted strings. Newlines are okay in triple quoted strings so things are easier.
Here's is an example on how to format a long query for better readability from your PR:
```
c.execute(
    """
    SELECT
        items.id,
        items.name,
        items.image,
        category.name
    FROM
        items
    INNER JOIN
        category
    ON
        items.category_id=category.id
    WHERE
        items.id IS ?
    """,
    id
)
```

* awesome (topic)