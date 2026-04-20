import React from "react"
export type homePageProp = {
    setLoginPageOpen: React.Dispatch<React.SetStateAction<boolean>>
}
interface homePageType {
    setLoginPageOpen: React.Dispatch<React.SetStateAction<boolean>>
    setSignupPageOpen: React.Dispatch<React.SetStateAction<boolean>>
}
const Homepage = ({ setLoginPageOpen,setSignupPageOpen }:homePageType) => {
  return (
    <div className="HomePageWrapper">
          <header className="HomeHeader">
              <nav className="HomeNav">
                  <button className="SignupBtn" onClick={() => setSignupPageOpen(true)}>Signup</button>
                  <button className="LoginBtn" onClick={() => setLoginPageOpen(true)}>Login</button>
              </nav>
          </header>
          <main className="HomeBody">
    <div className="HomeContent">
        <section className="HeroSection">
            <h1>Your DBMS Project Name</h1>
            <p>Short description of what your system actually does</p>
            <div className="HeroActions">
                <button className="PrimaryAction">Get Started</button>
                <button className="SecondaryAction">Learn More</button>
            </div>
        </section>
    </div>
</main>
    </div>
  )
}

export default Homepage