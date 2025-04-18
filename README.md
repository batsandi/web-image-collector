# web-image-collector
A simple API service collecting images from a selected website. It includes a docker compose project with two containers for the FastAPI app and a standard PostgreSQL. The service uses Selenium to crawl websites.

# Run Locally
Requires docker and docker compose

Clone the repository

```
git clone git@github.com:batsandi/web-image-collector.git
```
navigate inward

```
cd web-image-collector
```
rename `env.dev.sample` to `.env.dev` and optionally

```
mv .env.dev .env.dev.sample
```

>[!NOTE]
> Optionally rename the variables in the `.env.dev`. both the docker compose and the env files are geared towards development environment only, production setup would require a different approach

run the docker compose setup

```
docker compose -f docker-compose.dev.yaml up --build
```
The service should now be running on `localhost:8000`

example POST request to crawl a website.

```
curl -X POST "http://localhost:8000/screenshots" -H "Content-Type: application/json" -d '{"start_url": "https://noworkteambg.com", "n_links": 3}'
```
Use the returned `run_id` to pass to the following GET request

```
curl -X GET "http://localhost:8000/screenshots/<run_id>"
```
The service also has a `is_alive` endpoint at `/is_alive`

__Full API docs available at__:

http://127.0.0.1:8000/docs


## Action Plan
Using your favourite python framework implement a python service, responsible for collecting website screenshots (using puppeteer or playwright or selenium).
- [x] Install dependencies and create requirements.txt (Selenium, SQLALchemy, FastAPI, Pydantic)
Details about the service:
The service should support the following 3 routes:
- [x] GET /isalive - status check
- [x] POST /screenshots - 2 parameters (body): “start url” and “number of links to follow”. 
  - [x] The route response should be an unique id which later could be used with the GET /screenshots route to return the screenshots.
  - [x] screenshots saved on disk, id of the current run in the db
- [x] GET /screenshots/:id - return collected screenshots for the provided id

While developing the solution focus on following:
Performance
  - [x] Async crawling using `BackgroundTask` in FastAPI
How storing web page screenshots could be optimised:
- [ ] Compressing images using `Pillow`
- [ ] Store in cloud (to allow retrieval from clients)
How monitoring could be implemented and what is important to be monitored:
- [ ] Logging to file
- [x] Service to be able to run inside docker
  - [x] docker compose
  - [x] postgres
  - [x] collector

__Success criteria:__
- [x] Run the service and fire a POST request to start crawling of any site in the wild. (e.g. https://edited.com, 2)
- [x] Save screenshots for start url and first 2 links parsed from the html response of the homepage.
- [x] The code should be uploaded on git repo and link to be sent to email: sv**@***d.com.
