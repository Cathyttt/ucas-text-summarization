y = "this Terry Jones had a love of the absurd that contributed much to the anarchic humour of Monty Python's Flying Circus. His style of visual comedy, leavened with a touch of the surreal, inspired many comedians who followed him. It was on Python that he honed his directing skills, notably on Life of Brian and The Meaning of Life. A keen historian, he wrote a number of books and fronted TV documentaries on ancient and medieval history. Terence Graham Parry Jones was born in Colwyn Bay in north Wales on 1 February 1942. His grandparents ran the local amateur operatic society and staged Gilbert and Sullivan concerts on the town's pier each year His family moved to Surrey when he was four but he always felt nostalgic about his native land. \"I couldn't bear it and for the longest time I wanted Wales back,\" he once said. \"I still feel very Welsh and feel it's where I should be really.\" After leaving the Royal Grammar School in Guildford, where he captained the school, he went on to read English at St Edmund Hall, Oxford. However, as he put it, he \"strayed into history\", the subject in which he graduated. While at Oxford he wrote sketches for the Oxford Revue and performed alongside a fellow student, Michael Palin.\n"
with open("../raw_data/temp.raw_src") as file:
    for x in file:
        x = x.strip().lower()
        x = x.replace('[cls]','[CLS]').replace('[sep]','[SEP]')
        y = y.strip().lower()
        y = y.replace('[cls]','[CLS]').replace('[sep]','[SEP]')
        if x==y:
            print("aaaaaaaaa")
        print(x)
        print(y)

