# web-image-collector
A simple API service collecting images from a selected website

## Action Plan
Using your favourite python framework implement a python service, responsible for collecting website screenshots (using puppeteer or playwright or selenium).
- [ ] Install dependencies and create requirements.txt
  - [ ] Selenium
  - [ ] SQLAlchemy
  - [ ] FastAPI
Details about the service:
The service should support the following 3 routes:
- [ ] GET /isalive - 
- [ ] POST /screenshots - 2 parameters: “start url” and “number of links to follow”. 
  - [ ] The route response should be an unique id which later could be used with the GET /screenshots route to return the screenshots.
  - [ ] screenshots saved on disk, id of the current run in the db
- [ ] GET /screenshots/:id - return collected screenshots for the provided id

While developing the solution focus on following:
- [ ] Performance optimizations of the service
  - [ ] Async crawling using `BackgroundTask` in FastAPI
  - [ ] Multiple threads?
How storing web page screenshots could be optimised:
- [ ] Compressing images using `Pillow`
- [ ] Store in cloud (to allow retrieval from clients)
How monitoring could be implemented and what is important to be monitored:
- [ ] Logging
- [ ] Service to be able to run inside docker
  - [ ] docker compose
  - [ ] postgres
  - [ ] collector

__Success criteria:__
- [ ] Run the service and fire a POST request to start crawling of any site in the wild. (e.g. https://edited.com, 2)
- [ ] Save screenshots for start url and first 2 links parsed from the html response of the homepage.
- [ ] The code should be uploaded on git repo and link to be sent to email: sv**@***d.com.
