import 'package:graphql_flutter/graphql_flutter.dart';

Future<GraphQLClient> initGraphQLClient() async {
  await initHiveForFlutter(); // needed for cache storage

  final HttpLink httpLink = HttpLink(
    'http://127.0.0.1:8000/graphql', // backend endpoint
  );

  return GraphQLClient(
    cache: GraphQLCache(store: HiveStore()),
    link: httpLink,
  );
}