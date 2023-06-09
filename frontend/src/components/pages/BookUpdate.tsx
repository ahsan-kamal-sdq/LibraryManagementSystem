import { ReactElement, useState } from "react";
import { useHistory, useParams } from "react-router-dom";
import { useEffect } from "react";
import { client } from "../../axios";
import { BookOut, BookIn } from "../../CustomTypes";
import BookForm from "../BookForm";

/**
 * The BookUpdate component displays a form for updating book details.
 * @returns The component to be rendered
 */
function BookUpdate(): ReactElement {
  const history = useHistory();
  let { id }: { id: string } = useParams(); // id is extracted from url

  // Fetching the book to be edited
  let [currBook, setCurrBook]: [
    BookIn | undefined,
    React.Dispatch<React.SetStateAction<BookIn | undefined>>
  ] = useState();

  // This effect fetches the book
  useEffect(() => {
    client
      .GetBookDetails(id)
      .then((bookResponse: BookIn) => {
        let book: any = { ...bookResponse };
        setCurrBook(book);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [id]);

  /**
   * This function is called when user submits the form. It uses api call to
   * server and saves the changes that were made to book details.
   * Once updated, we navigate to the details page for the book.
   * @param book The updated details of the book that were entered into the form.
   */
  function submitHandler(book: BookOut) {
    if (currBook) {
      client
        .UpdateBook(book, currBook.id)
        .then((bookId) => {
          history.push("/books/" + currBook?.id);
        })
        .catch((error) => {
          alert(error);
        });
    } else {
      alert("Error! Book with this id does not exist");
    }
  }

  return (
    <div className='background-image'>
                <div className='modal'>

      {currBook !== undefined && (
        <BookForm book={currBook} submitHandler={submitHandler}></BookForm>
      )}
      {currBook === undefined && <p>Invalid Id!</p>}
    </div>
    </div>
  );
}

export default BookUpdate;
