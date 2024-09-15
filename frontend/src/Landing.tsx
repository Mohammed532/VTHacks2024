import { Link } from "react-router-dom"

function Landing() {
    const clickHandler:React.MouseEventHandler<HTMLButtonElement> = () => {

    }

    return (
        <div className="main">
            <div className="bg-primary h-2 shadow"></div>
            <div className="hero min-h-screen">
                <div className="hero-content text-center">
                    <div className="max-w-md">
                        <h1 className="text-9xl text-primary">Logo</h1>
                        <p className="text-xl py-14">A motto is indeed needed I guess</p>
                        <Link to={'home'} role="button" className="btn btn-primary">Get Started</Link>
                    </div>
                </div>
            </div>
        </div>        
    )

}

export default Landing
