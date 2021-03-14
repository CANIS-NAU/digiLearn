const VERSION = '{{ version }}'

self.addEventListener('install', (event) => 
{
    console.log('[SW] Installing SW version:', VERSION)
});



// TODO

// add ofline functionality by caching the base webpage in the service Worker

// Take in user input data and add them to a local storage queue

// when connection is made, push items in the local storae queue and delete them from there

// look into authentication might be important idk