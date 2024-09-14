
type FileDrawerProp = {
    title: string,
    files: [],
    addFileButton?: boolean
    className?: string
}

export default function FileDrawer({ title, className }: FileDrawerProp){
    return(
        <div className={`${className}`}>
            <div className="flex flex-row justify-between items-center m-2">
                <h3 className="text-2xl font-medium">{title}</h3>
                <button className="btn btn-secondary p-1">+</button>
            </div>
            <div className="bg-secondary rounded min-h-[30vh] overflow-x-scroll">
            </div>
        </div>
    )
}