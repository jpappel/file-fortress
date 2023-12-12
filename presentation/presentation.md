---
title: "File Fortress"
author:
- "JP Appel"
- "Owen Halliday"
- "David Marrero"
---

![](http://filefortress.xyz/logo-inverted){width=500px, height=500}

# File Hosting

::: {.flex}

:::: {.col}
![](http://filefortress.xyz/imgur){width=420px, height=100}
::::

:::: {.col}
![](http://filefortress.xyz/imgbb){width=420px, height=200} 
::::

:::

::: notes
Owen

* describe problem
* describe existing solutions (imgur, imgbb, etc)
* describe problems with existing solutions
:::

# Architecture

<!-- TODO: include updated diagram -->
![](http://filefortress.xyz/diagram){width=820px, height=400} 

::: notes
JP

* this application is relatively portable
* everything is running in a docker container
* client requests hit nginx which redirects as necessary
* gunicorn used as wsgi server
* flask backend, connects directly mariadb container and block storage volume
:::


# Deployment

![](http://filefortress.xyz/docker){width=820px, height=300} 

. . .

```bash
docker compose up -d
docker compose down -v
```

::: notes
JP

* you may wonder how we manage deployment with a stack as seen on the slide prior
* docker compose allows us to start and stop our application with a single command
* in repo a script is provided to deploy on an ec2 instances running amazon linux
* for today's demo we are running on one of owen's machines
    * this is to avoid having to transfer our https certificates
:::

# Interfaces

## Web
<iframe data-src="http://filefortress.xyz" height="500px" width="700px"></iframe>

## API

```
GET /api/v1/file/<short_link>
GET /api/v1/file/<short_link>/info
OPTIONS /api/v1/file/<short_link>
POST /api/v1/file/<short_link>
DELETE /api/v1/file/<short_link>
```

## CLI

# Demo
<img alt="Picture of the Class" src="http://filefortress.xyz/class"></img>


# GitHub Workflows

![](http://filefortress.xyz/i_love_tests)

::: notes
Owen

:::

# 

![](http://filefortress.xyz/nginx)

::: notes
JP

* a way that our architecture differs from other groups is Nginx
* nginx is a reverse proxy and web server known for its speed
* by placing nginx at the edge of our network we can change internal network interfaces without affecting the client
* additionally nginx provides additional features such as
    * limiting upload size
    * automatically redirecting http traffic to https
    * faster serving of static files
:::

# Lessons Learned

* test, test, test!
* mocking correctly is difficult

# Future Work

::: incremental
* authentication
    * privacy settings
* S3/Object Storage
* HTTPS
* collections
:::
