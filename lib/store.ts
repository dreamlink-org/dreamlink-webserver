import { promises as fs, createReadStream, createWriteStream } from "fs"
import { join } from "path"
import { rootDirectory } from "./root"
import { Readable, Writable } from "stream"

type DataStore = {
    checkData(key : string) : Promise<boolean>
    getData(key : string, target: Writable) : Promise<void>
    setData(key : string, source : Readable) : Promise<void>
    deleteData(key : string) : Promise<void>
}

export class LocalStore implements DataStore {

    storePath : string

    constructor(storePath : string) {
        this.storePath = storePath
    }

    checkData = async (key: string): Promise<boolean> => {
        const joinedPath = join(this.storePath, key)
        return await fs.access(joinedPath).then(() => true).catch(() => false)
    }

    getData = async (key: string, target: Writable): Promise<void> => {
        await new Promise((rs,rj) => {
            const joinedPath = join(this.storePath, key)
            const readStream = createReadStream(joinedPath)
            readStream.pipe(target)
            readStream.on("end", rs)
            readStream.on("error", rj)
        })
    }

    setData = async (key: string, source: Readable): Promise<void> => {
        await new Promise((rs,rj) => {
            const joinedPath = join(this.storePath, key)
            const writeStream = createWriteStream(joinedPath)
            source.pipe(writeStream)
            writeStream.on("finish", rs)
            writeStream.on("error", rj)
        })
    }

    deleteData = async (key: string): Promise<void> => {
        const joinedPath = join(this.storePath, key)
        await fs.unlink(joinedPath)
    }

}

const localPath = join(rootDirectory, "store")
export const store = new LocalStore(localPath)