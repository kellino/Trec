#!/usr/bin/sh

TERRIER_HOME=$(find ~/ -type d -name "terrier-core*")
CLUEWEB=$(find ~/ -type d -name "clueweb*")
QRELS_ADHOC=$(find ~/ -type f -name "qrels.adhoc.*")
TREC_TOPICS=$(find ~/ -type f -name "trec*topics.*")

terrier_home() {
    if [ -e "$TERRIER_HOME" ]; then
        echo "terrier home found at $TERRIER_HOME"
    else
        echo "TERRIER_HOME not found" && exit
    fi
}

clueweb_home() {
    if [ -e "$CLUEWEB" ]; then
        echo "clueweb found at $CLUEWEB"
    else
        echo "clueweb directory not found" && exit
    fi
}

terrier_setup() {
    "$TERRIER_HOME"/bin/trec_setup.sh "$CLUEWEB"
    find "$CLUEWEB" -type f | sort | grep -v info > "$TERRIER_HOME"/etc/collection.spec
}

append_settings() {
    if [ -e "$QRELS_ADHOC" ] && [ -e "$TREC_TOPICS" ]; then
# the indentation here is very ugly, but it helps to avoid any issues with tabs vs whitespace
cat <<- EOF >> "$TERRIER_HOME"/etc/terrier.properties
trec.collection.class=SimpleFileCollection
indexing.simplefilecollection.extensionsparsers=txt:TaggedDocument
indexer.meta.forward.keys=docno
indexer.meta.forward.keylens=26
indexer.meta.reverse.keys=docno
TrecDocTags.skip=script, style
trec.qrels=$QRELS_ADHOC
trec.topics=$TREC_TOPICS
trec.model=org.terrier.matching.models.BM25
TrecQueryTags.doctag=title
TrecQueryTags.idtag=num
EOF
        echo "collection.spec updated"
        else
            echo "unable to update collection.spec"
        fi
} 

make_index() {
    "$TERRIER_HOME/bin/trec_terrier.sh -i -j"
}

terrier_home && clueweb_home && terrier_setup && append_settings
