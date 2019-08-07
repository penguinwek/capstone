import React from 'react'
import { S3 } from 'aws-sdk'

const accessKeyId = 'AKIAWU5KMJHA6YDCYV3X'
const secretAccessKey = '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'
const region = 'ap-southeast-1'

const s3 = new S3({
    secretAccessKey,
    accessKeyId,
    region
})

export default () => {
    const fileRef = React.useRef<HTMLInputElement>(null)

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        try {
            if (!fileRef.current || !fileRef.current.files) return
            const file = fileRef.current.files[0]

            const url = await makeSignedURL({filename: file.name, filetype: file.type})
            console.log('A name was submitted', url)

            await uploadToS3(url, file)

        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div>
            Hello, World!

            <form method='post' onSubmit={(event) => handleSubmit(event)}>
                <label>
                    Upload file to S3:
                    <input type="file" name="file-upload" ref={fileRef}/>
                </label>
                <input type="submit" value="Submit"/>  
            </form>
        </div>
    )
} 

interface makeSignedURLArgs {
    filename: string,
    filetype: string
}

const makeSignedURL = async ({filename, filetype}: makeSignedURLArgs): Promise<string> => {
    const signedUrl = await new Promise((resolve: (value: string) => void, reject) => {
        const signedUrlExpireSeconds = 60 * 60;
        s3.getSignedUrl('putObject', {
            Expires: signedUrlExpireSeconds, 
            Bucket: 'capstone-robekoc',
            // Path: '/uploads/',
            Key: filename, 
            ACL: 'bucket-owner-full-control',
            ContentType: filetype
        }, (err, url) => {
            if (err) {
                console.log("AHHHHHHHHH")
                reject(err)
            }
            resolve(url) 
        })
    })
    
    return signedUrl
}

const uploadToS3 = async (url: string, file: File) => {
    await fetch(url, {body: file, method: "PUT", headers: {"Content-Type": file.type}})
}