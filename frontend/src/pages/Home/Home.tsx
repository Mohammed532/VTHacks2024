import { Header, FileDrawer } from './../../ui'
import { ChangeEventHandler, MouseEventHandler, useState } from 'react'
import { useURLFile } from '../../hooks'

export default function Home(){
    const [clutteredImgs, setClutteredImgs] = useState<string[]>([]);
    const [declutterdImgs, setDeclutteredImgs] = useState<string[]>([])
    const [file, pending, err] = useURLFile('https://replicate.delivery/pbxt/ZgoZKKZfhxRevEVIxpPWFMincBdrPdxiMNEAIrz7PoU9IAdTA/remove_anthing.png', 'test')
    
    let onClitterImgUpdate: ChangeEventHandler<HTMLInputElement> = (e) => {
        let files = e.target.files
        let img_urls: string[] = [];
        if(files){
            for(let i = 0; i < files.length; i++){
                img_urls.push(URL.createObjectURL(files.item(i) as File))
            }   
        }
        setClutteredImgs(img_urls)
        
    }

    let generateDeclutteredImgs: MouseEventHandler<HTMLButtonElement> = (e) => {
        let img_urls: string[] = [];
        if(!pending){
            img_urls.push(URL.createObjectURL(file as File))
        }
        setDeclutteredImgs(img_urls)
    }

    return(
        <div className="home">
            <Header />
            <div className="grid grid-cols-2 w-screen gap-4 pt-10"> 
                <FileDrawer className="basis-1/2 m-6" title="Images" files={clutteredImgs} fileChangeFn={onClitterImgUpdate}/>
                <FileDrawer className="basis-1/2 m-6 hidden" title="Floorplan" files={[]}/>
            </div>
            <button className={`btn ${clutteredImgs.length ? 'btn-primary' : 'btn-disabled'} m-6`} onClick={generateDeclutteredImgs}>Generate</button>
            <div className="flex justify-center">
                <div className="divider divider-secondary w-11/12 text-center"></div>
            </div>
            <FileDrawer className='m-6' title='Decluttered Images' files={declutterdImgs} />
            <button className='btn btn-disabled m-6'>Download ZIP</button>

        </div>
    )
}