FROM node:latest

WORKDIR /app

COPY package.json tsconfig.json src ./

RUN npm install --save

CMD ["npm", "run", "prod"]