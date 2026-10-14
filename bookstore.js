// Step 2: switch to the bookstore database
// (use bookstore only works at the mongosh prompt)
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list every author and every book
printjson(db.authors.find().toArray())
printjson(db.books.find().toArray())

// Step 6: insert two new books
db.books.insertOne({ title: "Dune", published_year: 1965, author_ids: ["author_004"] })
db.books.insertOne({ title: "Coraline", published_year: 2002, author_ids: ["author_002"] })

// Step 7: add the missing author (author_004)
db.authors.insertOne({
  _id: "author_004",
  name: "Frank Herbert",
  nationality: "American",
  bio: {
    short: "American science fiction author best known for Dune.",
    long: "Frank Herbert (1920-1986) was an American writer and journalist. His 1965 novel Dune became one of the best-selling science fiction novels of all time and launched a series of sequels."
  }
})

// Step 8: filter books by a list of authors
printjson(db.books.find({ author_ids: { $in: ["author_001", "author_004"] } }).toArray())
