import { Link } from "react-router-dom"

function Landing() {
    return (
        <div className="main">
            <div className="bg-primary h-2 shadow"></div>
            <div className="hero min-h-screen">
                <div className="hero-content text-center">
                    <div className="">
                        <h1 className="text-9xl text-primary">Clear View AI</h1>
                        <p className="text-xl py-14">The tool you need for some Clear View</p>
                        <Link to={'home'} role="button" className="btn btn-primary">Get Started</Link>
                    </div>
                </div>
            </div>
        </div>        
    )

}

export default Landing
