const apiConfig = {
    baseUrl: 'https://api.themoviedb.org/3/',
    apiKey: 'fa4b9bed6aa4caf0c8cc3e59eb26751d',
    originalImage: (imgPath) => `https://image.tmdb.org/t/p/original/${imgPath}`,
    w500Image: (imgPath) => `https://image.tmdb.org/t/p/w500/${imgPath}`
}

export default apiConfig;