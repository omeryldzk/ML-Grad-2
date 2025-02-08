import {Outlet} from "react-router-dom"

export const Layout = () => {
    return (
        <>
            <div className="main-body">
                <Outlet />
            </div>
        </>
    )
}