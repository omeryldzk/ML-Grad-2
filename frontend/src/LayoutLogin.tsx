import {Outlet} from "react-router-dom"

export const LayoutLogin = () => {
    return (
        <>
            <div className="main-body">
                <Outlet />
            </div>
        </>
    )
}