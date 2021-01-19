FROM node:latest

WORKDIR /app

COPY package.json tsconfig.json src ./

RUN npm install --save

ENV MONGO_URL "mongodb+srv://schedulerUser:secretPassword6345346@brcluster.w7xjc.mongodb.net/scheduler?retryWrites=true&w=majority"

CMD ["npm", "run", "prod"]