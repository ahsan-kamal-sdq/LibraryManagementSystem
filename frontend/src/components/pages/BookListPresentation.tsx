import React, { useState } from "react";
import { Link } from "react-router-dom";
import { BookIn } from "../../CustomTypes";
import LibrarianLinks from "../LibrarianLinks";
import "../style.css"; // Import the Genres CSS file
import ScrollView from "../Scrollview";
import { Pagination } from "./pagination";

export const BookListPresentation = (props: {
  books: BookIn[];
  url: string;
  showLinks: boolean;
  page: number;
  setPage: React.Dispatch<React.SetStateAction<number>>;
}) => {
  const [searchTerm, setSearchTerm] = useState<string>(""); // State for the search term

  // Filtered books based on search term
  const filteredBooks = props.books.filter((book) =>
    book.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <h1>Books</h1>
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-evenly",
        }}
      >
        <div>
          <h3>Search Book: </h3>
        </div>
        <div style={{ marginTop: 18 }}>
          <input
            type="text"
            placeholder="Search books..."
            value={searchTerm}
            onChange={handleSearchChange}
          />
        </div>
      </div>
      <br />
      <ScrollView>
        <div className="card-container">
          {filteredBooks.map((book) => (
            <div
              key={book.id.toString()}
              className="card"
              data-testid={"item" + book.id.toString()}
            >
              <Link to={"/books/" + book.id.toString()}>{book.title}</Link>
              <p>
                <b>Authors:</b>
              </p>
              <p>
                {book.authors
                  .map((author) => {
                    return ` ${author.first_name} ${author.last_name}`;
                  })
                  .join(", ")}
              </p>
              <p>
                <b>Description :</b>
              </p>
              <p>{book.description}</p>
            </div>
          ))}
        </div>
      </ScrollView>
      {props.showLinks && (
        <div style={{ display: "flex", justifyContent: "center" }}>
          <div>
            <Link to={`${props.url}/create`} className="genre-link">
              {" "}
              Create Book{" "}
            </Link>
          </div>
        </div>
      )}
      <Pagination
        page={props.page}
        setPage={props.setPage}
        showNext={props.books.length === 10}
      />
    </>
  );
};
