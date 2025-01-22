#https://medium.com/@koiralanet/setup-next-js-project-with-turbo-docker-eslint-prettier-ci-pipeline-and-tailwind-css-a7d9fd99199d


# Dockerfile pour le frontend React depuis image node
FROM node:22-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package*.json ./

# Copier les fichiers de l'application
COPY . .

# Dépendances
RUN npm install

# Exposer le port de l'application
EXPOSE 3000

# Lancement de l'app
CMD ["npm", "run", "dev"]
