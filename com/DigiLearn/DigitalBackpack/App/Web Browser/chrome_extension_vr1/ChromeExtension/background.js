// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

const app = firebase.initializeApp(config);
const auth = app.auth();
const signInWithPopup = () => {
  const provider = new firebase.auth.GoogleAuthProvider();
  return auth.signInWithPopup(provider).catch((error) => {
    console.log(error);
  });
};