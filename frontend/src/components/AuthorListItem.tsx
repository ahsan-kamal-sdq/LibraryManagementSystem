import React, { useContext } from "react";
import { Link, useRouteMatch } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import { Author } from "../CustomTypes";

// The attributes of a single author

// The properties received by this component
export type AuthorListItemProps = {
  key: number;
  item: Author;
  linksto: string;
};

function AuthorListItem(props: AuthorListItemProps) {
  /**
   * This takes an author object as a prop and
   * Renders out the details to be displayed on the author list page
   */
  const { url }: { url: string } = useRouteMatch();
  const { isLibrarian }: { isLibrarian: boolean } = useContext(AuthContext);

  //This function runs if the current user is a librarian. i.e has permission to edit or delete an authors details
  function librarianLinks() {
    return (
      <>
        <Link to={`${url}/${props.item.id}/update`} style={{ color: "orange" }}>
          {" "}
          Update{" "}
        </Link>
        <Link to={`${url}/${props.item.id}/delete`} style={{ color: "red" }}>
          Delete
        </Link>
      </>
    );
  }

  return (
    <>
      <Link to={props.linksto}>
        {props.item.last_name}, {props.item.first_name}
        <br></br>
        <br></br>
        <span>
          {"("}
          <span style={{ fontWeight: "bold" }}>
            {props.item.birth_date == null
              ? "--"
              : props.item.birth_date.substring(0, 10).replace(/-/g, "/")}
          </span>{" "}
          -{" "}
          <span style={{ fontWeight: "bold" }}>
            {props.item.death_date == null
              ? "--"
              : props.item.death_date.substring(0, 10).replace(/-/g, "/")}
          </span>
          {")"}
        </span>
        <br></br>
        <br></br>
      </Link>
      {isLibrarian === true ? librarianLinks() : null}
    </>
  );
}

export default AuthorListItem;
