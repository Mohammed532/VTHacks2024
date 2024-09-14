import { Header, FileDrawer } from './../../ui'

export default function Home(){
    return(
        <div className="home">
            <Header />
            <div className="flex flex-row w-screen gap-4 pt-10"> 
                <FileDrawer className="basis-1/2 m-6" title="Images" files={[]}/>
                <FileDrawer className="basis-1/2 m-6" title="Floorplan" files={[]}/>
            </div>
            <button className='btn btn-primary m-6'>Generate</button>
            <div className="flex justify-center">
                <div className="divider divider-secondary w-11/12 text-center"></div>
            </div>
            <FileDrawer className='m-6' title='Decluttered Image' files={[]} />
            <button className='btn btn-disabled m-6'>Download ZIP</button>

        </div>
    )
}