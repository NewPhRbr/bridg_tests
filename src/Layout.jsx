import { Outlet } from "react-router-dom";
import Nav from "./Nav";

export default function Layout() {
  return (
    <>
      <Nav />
      <div className="container-fluid">
        <Outlet />
      </div>
    </>
  );
}