import './App.css'
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import {LayoutLogin} from "./LayoutLogin.tsx";
import {Layout} from "./Layout.tsx";
import Home from "./pages/Home.tsx";
import SelectProgram from "./pages/SelectProgram.tsx";


function App() {


  return (
      <Router>
        <Routes>
          <Route element={<LayoutLogin />}>

          </Route>


          <Route element={<Layout/>}>

            <Route path= "/"
                   element={
                        <Home/>
                   }/>

            <Route path={"/selectProgram"}
                   element={
                        <SelectProgram />
                   }/>

          </Route>


        </Routes>
      </Router>


  )
}

export default App
