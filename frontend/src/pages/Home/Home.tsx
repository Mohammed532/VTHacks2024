import { Header, FileDrawer } from './../../ui'
import { ChangeEventHandler, MouseEventHandler, useState } from 'react'
import { useURLFile, useZip } from '../../hooks'
import axios from 'axios'

export default function Home(){
    const [clutteredImgs, setClutteredImgs] = useState<string[]>([]);
    const [clutterdRaw, setClutteredRaw] = useState<FileList | null>(null);
    const [declutterdImgs, setDeclutteredImgs] = useState<string[]>([]);
    const [declutterdRaw, setDeclutteredRaw] = useState<FileList | File[] | null>(null);
    const [file, pending, err] = useURLFile('https://replicate.delivery/pbxt/2gkSoW0o7ALGDdPiipfmBbwlyJzSZMElBWtXked5AQ0KNCdTA/remove_anthing.png', 'test')
    const createZipFn = useZip('file');
    
    let onClitterImgUpdate: ChangeEventHandler<HTMLInputElement> = (e) => {
        let files = e.target.files;
        setClutteredRaw(files);
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
        const data = new FormData();
        
        if(clutterdRaw){
            for(let i = 0; i < clutterdRaw.length; i++){
                data.append('files', clutterdRaw.item(i) as File);
            }
        }
        
        axios.post('http://127.0.0.1:5000/upload', data)
          .then(res => {
            // TODO: implement 
          })
          .catch(err => {
            console.log(err);
          })


        if(!pending){
            setDeclutteredRaw([file as File])
            img_urls.push(URL.createObjectURL(file as File))
        }
        setDeclutteredImgs(img_urls)
    }

    let startZipDownload = () => {
        if (declutterdRaw) {
            createZipFn(declutterdRaw)
        }
    }

    return(
        <div className="home">
            <Header />
            <div className="grid grid-cols-2 w-screen gap-4 pt-10"> 
                <FileDrawer className="basis-1/2 m-6" title="Images" files={clutteredImgs} fileChangeFn={onClitterImgUpdate} addFileButton={true}/>
                <FileDrawer className="basis-1/2 m-6 hidden" title="Floorplan" files={[]}/>
            </div>
            <button className={`btn ${clutteredImgs.length ? 'btn-primary' : 'btn-disabled'} m-6`} onClick={generateDeclutteredImgs}>Generate</button>
            <div className="flex justify-center">
                <div className="divider divider-secondary w-11/12 text-center"></div>
            </div>
            <FileDrawer className='m-6' title='Decluttered Images' files={declutterdImgs} />
            <button className={`btn ${declutterdImgs && declutterdRaw ? 'btn-primary' : 'btn-disabled'} m-6`} onClick={startZipDownload}>Download ZIP</button>

        </div>
    )
}