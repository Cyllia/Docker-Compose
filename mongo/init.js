db = db.getSiblingDB('blog_db');

db.posts.insertMany([
  { title: "Post 1" },
  { title: "Post 2" },
  { title: "Post 3" },
  { title: "Post 4" },
  { title: "Post 5" }
]);